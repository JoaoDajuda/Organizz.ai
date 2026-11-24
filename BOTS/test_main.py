import unittest
from unittest.mock import AsyncMock, patch

from BOTS import main
from langchain_core.messages import AIMessageChunk


class ConversationActionTests(unittest.IsolatedAsyncioTestCase):
    async def test_event_request_asks_for_missing_time_then_creates_event(self):
        class NoModelCall:
            async def astream(self, _messages):
                raise AssertionError("A solicitação explícita não deve depender do modelo.")
                yield

        payload = main.ChatRequest(input=[
            main.MessageItem(
                id="turn-1",
                sender="user",
                content="Tenho um casamento para o dia 24 de novembro",
            ),
            main.MessageItem(
                id="turn-1",
                sender="bot",
                content="Certo.",
            ),
            main.MessageItem(
                id="turn-2",
                sender="user",
                content="Crie um agendamento para casamento na data especificada",
            ),
        ])
        backend = AsyncMock(return_value={"id_agenda": 18})
        with (
            patch.object(main, "_hoje_local", return_value=main.date(2099, 1, 1)),
            patch.object(main, "llm_with_tools", NoModelCall()),
            patch.object(main, "request_backend", backend),
        ):
            pending, prompt = await main._processar_turno(payload, {}, "token", None)
            self.assertEqual(pending["kind"], "create_agenda_draft")
            self.assertIn("horário", prompt)
            backend.assert_not_awaited()

            followup = main.ChatRequest(input=[
                *payload.input,
                main.MessageItem(id="turn-3", sender="user", content="15:30"),
            ])
            cleared, reply = await main._processar_turno(
                followup, {}, "token", pending
            )

        self.assertIsNone(cleared)
        self.assertIn("agendado", reply)
        backend.assert_awaited_once_with(
            "POST",
            "/agendas",
            "token",
            {
                "titulo": "casamento",
                "data": "2099-11-24T15:30",
                "data_fim": None,
                "dia_inteiro": False,
            },
        )

    async def test_event_creation_requires_a_valid_future_datetime(self):
        backend = AsyncMock()
        with (
            patch.object(main, "_hoje_local", return_value=main.date(2099, 1, 1)),
            patch.object(main, "request_backend", backend),
        ):
            pending, prompt = await main._preparar_acao(
                {
                    "name": "criar_compromisso",
                    "args": {
                        "titulo": "Consulta",
                        "data": "2026-02-31T15:00",
                    },
                },
                "token",
            )

        self.assertEqual(pending["kind"], "create_agenda_draft")
        self.assertIn("data não é válida", prompt)
        backend.assert_not_awaited()

    async def test_yearless_past_event_date_asks_for_year(self):
        payload = main.ChatRequest(input=[
            main.MessageItem(
                id="turn-1",
                sender="user",
                content="Agende consulta para 24 de novembro às 15h",
            ),
        ])
        backend = AsyncMock()
        with (
            patch.object(main, "_hoje_local", return_value=main.date(2099, 12, 1)),
            patch.object(main, "request_backend", backend),
        ):
            pending, prompt = await main._processar_turno(
                payload, {}, "token", None
            )

        self.assertEqual(pending["kind"], "create_agenda_draft")
        self.assertIn("qual ano", prompt.casefold())
        backend.assert_not_awaited()

    def test_expense_terms_map_to_the_frontend_categories(self):
        examples = {
            "comida": "Alimentação",
            "lanche": "Alimentação",
            "restaurante": "Alimentação",
            "aluguel": "Moradia",
            "conta de luz": "Moradia",
            "uber": "Transporte",
            "gasolina": "Transporte",
            "remédio": "Saúde",
            "farmácia": "Saúde",
            "cinema": "Lazer",
            "streaming": "Lazer",
            "curso": "Educação",
            "material escolar": "Educação",
            "presente": "Outros",
        }
        for term, expected in examples.items():
            with self.subTest(term=term):
                self.assertEqual(main._normalizar_categoria(term), expected)

    async def test_natural_expense_request_uses_amount_and_category_from_message(self):
        class NoModelCall:
            async def astream(self, _messages):
                raise AssertionError("A frase explícita não deve depender do modelo.")
                yield

        payload = main.ChatRequest(input=[
            main.MessageItem(
                id="turn-1",
                sender="user",
                content="Niza, gastei 4 reais de alimentação hoje",
            ),
        ])
        backend = AsyncMock(return_value={"id": 13})
        with (
            patch.object(main, "llm_with_tools", NoModelCall()),
            patch.object(main, "request_backend", backend),
        ):
            pending, reply = await main._processar_turno(payload, {}, "token", None)

        self.assertIsNone(pending)
        self.assertIn("R$ 4,00", reply)
        backend.assert_awaited_once_with(
            "POST",
            "/valores",
            "token",
            {
                "tipo_valor": "Saida",
                "valor": 4.0,
                "categoria": "Alimentação",
            },
        )

    async def test_spoken_food_synonym_is_saved_as_alimentacao(self):
        payload = main.ChatRequest(input=[
            main.MessageItem(
                id="turn-1",
                sender="user",
                content="Gastei 12 reais com lanche",
            ),
        ])
        backend = AsyncMock(return_value={"id": 14})
        with patch.object(main, "request_backend", backend):
            pending, reply = await main._processar_turno(payload, {}, "token", None)

        self.assertIsNone(pending)
        self.assertIn("registrada", reply)
        self.assertEqual(backend.await_args.args[3]["categoria"], "Alimentação")

    async def test_followup_amount_completes_saved_movement_draft(self):
        class NoModelCall:
            async def astream(self, _messages):
                raise AssertionError("A resposta do rascunho não deve depender do modelo.")
                yield

        payload = main.ChatRequest(input=[
            main.MessageItem(id="turn-1", sender="user", content="Gastei com alimentação"),
            main.MessageItem(id="turn-1", sender="bot", content="Qual foi o valor?"),
            main.MessageItem(id="turn-2", sender="user", content="4 reais"),
        ])
        pending = main._novo_pendente(
            "create_value_draft",
            {"tipo_valor": "Saida", "valor": None, "categoria": "alimentação"},
            "",
        )
        backend = AsyncMock(return_value={"id": 13})
        with (
            patch.object(main, "llm_with_tools", NoModelCall()),
            patch.object(main, "request_backend", backend),
        ):
            new_pending, reply = await main._processar_turno(
                payload, {}, "token", pending
            )

        self.assertIsNone(new_pending)
        self.assertIn("R$ 4,00", reply)
        backend.assert_awaited_once_with(
            "POST",
            "/valores",
            "token",
            {
                "tipo_valor": "Saida",
                "valor": 4.0,
                "categoria": "Alimentação",
            },
        )

    async def test_malformed_tool_json_is_not_exposed_in_chat(self):
        class BrokenToolOutput:
            async def astream(self, _messages):
                yield AIMessageChunk(
                    content='{"name":"criar_movimentacao","parameters{',
                )

        payload = main.ChatRequest(input=[
            main.MessageItem(id="turn-1", sender="user", content="4 reais"),
        ])
        with patch.object(main, "llm_with_tools", BrokenToolOutput()):
            pending, reply = await main._processar_turno(payload, {}, "token", None)

        self.assertIsNone(pending)
        self.assertNotIn('"name"', reply)
        self.assertIn("repetir", reply)

    async def test_llm_tool_call_dispatches_only_to_allowed_backend_route(self):
        class FakeRunnable:
            async def astream(self, _messages):
                yield AIMessageChunk(
                    content="",
                    tool_call_chunks=[{
                        "name": "listar_movimentacoes",
                        "args": "{}",
                        "id": "call-1",
                        "index": 0,
                    }],
                )

        payload = main.ChatRequest(input=[
            main.MessageItem(id="turn-1", sender="user", content="Liste meus saldos."),
        ])
        backend = AsyncMock(return_value=[])
        with (
            patch.object(main, "llm_with_tools", FakeRunnable()),
            patch.object(main, "request_backend", backend),
        ):
            pending, reply = await main._processar_turno(
                payload, {}, "token", None
            )

        self.assertIsNone(pending)
        self.assertIn("Não encontrei", reply)
        backend.assert_awaited_once_with("GET", "/valores", "token")

    async def test_create_movement_uses_finance_route(self):
        backend = AsyncMock(return_value={"id": 13})
        with patch.object(main, "request_backend", backend):
            pending, prompt = await main._preparar_acao(
                {
                    "name": "criar_movimentacao",
                    "args": {
                        "tipo_valor": "Saida",
                        "valor": 22.5,
                        "categoria": "Alimentação",
                        "data": "2026-11-17",
                    },
                },
                "token",
            )
        self.assertIsNone(pending)
        self.assertIn("registrada", prompt)
        backend.assert_awaited_once_with(
            "POST",
            "/valores",
            "token",
            {
                "tipo_valor": "Saida",
                "valor": 22.5,
                "categoria": "Alimentação",
                "data": "2026-11-17",
            },
        )

    async def test_missing_expense_category_does_not_call_backend(self):
        backend = AsyncMock()
        with patch.object(main, "request_backend", backend):
            pending, reply = await main._preparar_acao(
                {
                    "name": "criar_movimentacao",
                    "args": {"tipo_valor": "Saida", "valor": 22.5},
                },
                "token",
            )
        self.assertEqual(pending["kind"], "create_value_draft")
        self.assertIn("categoria", reply)
        backend.assert_not_awaited()

    async def test_delete_movement_requires_explicit_confirmation(self):
        backend = AsyncMock(return_value=[
            {
                "id": 7,
                "tipo_valor": "Saida",
                "valor": 22.5,
                "categoria": "alimentação",
                "data_movimentacao": "2026-11-17T00:00:00",
            },
        ])
        with patch.object(main, "request_backend", backend):
            pending, prompt = await main._preparar_acao(
                {
                    "name": "excluir_movimentacao",
                    "args": {"categoria": "comida"},
                },
                "token",
            )
            self.assertIn("Confirma", prompt)
            backend.assert_awaited_once_with("GET", "/valores", "token")
            backend.reset_mock()
            cleared, reply = await main._responder_pendente(pending, "confirmo", "token")

        self.assertIsNone(cleared)
        self.assertIn("excluída", reply)
        backend.assert_awaited_once_with("DELETE", "/valores/7", "token")

    async def test_ambiguous_delete_only_asks_for_clarification(self):
        backend = AsyncMock(return_value=[
            {"id": 7, "tipo_valor": "Saida", "valor": 22.5, "categoria": "mercado"},
            {"id": 8, "tipo_valor": "Saida", "valor": 34.0, "categoria": "mercado"},
        ])
        with patch.object(main, "request_backend", backend):
            pending, reply = await main._preparar_acao(
                {
                    "name": "excluir_movimentacao",
                    "args": {"categoria": "mercado"},
                },
                "token",
            )

        self.assertIsNone(pending)
        self.assertIn("mais de uma", reply)
        backend.assert_awaited_once_with("GET", "/valores", "token")

    async def test_mark_agenda_requires_confirmation(self):
        backend = AsyncMock(return_value=[
            {
                "id_agenda": 42,
                "titulo": "Reunião",
                "data": "2026-11-17T10:00",
                "status": "pendente",
            },
        ])
        with patch.object(main, "request_backend", backend):
            pending, prompt = await main._preparar_acao(
                {
                    "name": "marcar_compromisso",
                    "args": {"titulo": "reuniao"},
                },
                "token",
            )
            self.assertIn("Confirma", prompt)
            backend.assert_awaited_once_with("GET", "/agendas", "token")
            backend.reset_mock()
            cleared, reply = await main._responder_pendente(pending, "sim", "token")

        self.assertIsNone(cleared)
        self.assertIn("concluído", reply)
        backend.assert_awaited_once_with(
            "PATCH", "/agendas/42", "token", {"status": "concluida"}
        )

    async def test_unmark_agenda_returns_it_to_pending_after_confirmation(self):
        backend = AsyncMock(return_value=[
            {
                "id_agenda": 43,
                "titulo": "Consulta",
                "data": "2026-11-18T10:00",
                "status": "concluida",
            },
        ])
        with patch.object(main, "request_backend", backend):
            pending, prompt = await main._preparar_acao(
                {
                    "name": "desmarcar_compromisso",
                    "args": {"titulo": "Consulta"},
                },
                "token",
            )
            self.assertIn("Confirma", prompt)
            backend.reset_mock()
            cleared, reply = await main._responder_pendente(pending, "pode", "token")

        self.assertIsNone(cleared)
        self.assertIn("pendente", reply)
        backend.assert_awaited_once_with(
            "PATCH", "/agendas/43", "token", {"status": "pendente"}
        )

    async def test_cancel_does_not_call_backend(self):
        backend = AsyncMock()
        pending = {
            "kind": "delete_value",
            "args": {"id": 7},
            "description": "movimentação",
            "expires_at": main.monotonic() + 120,
        }
        with patch.object(main, "request_backend", backend):
            cleared, reply = await main._responder_pendente(pending, "não", "token")

        self.assertIsNone(cleared)
        self.assertIn("não fiz nenhuma alteração", reply)
        backend.assert_not_awaited()

    async def test_expired_confirmation_does_not_call_backend(self):
        backend = AsyncMock()
        pending = {
            "kind": "delete_value",
            "args": {"id": 7},
            "description": "movimentação",
            "expires_at": 0,
        }
        with patch.object(main, "request_backend", backend):
            cleared, reply = await main._responder_pendente(pending, "sim", "token")

        self.assertIsNone(cleared)
        self.assertIn("expirou", reply)
        backend.assert_not_awaited()

    async def test_ambiguous_confirmation_cancels_without_calling_backend(self):
        backend = AsyncMock()
        pending = {
            "kind": "delete_value",
            "args": {"id": 7},
            "description": "movimentação",
            "expires_at": main.monotonic() + 120,
        }
        with patch.object(main, "request_backend", backend):
            cleared, reply = await main._responder_pendente(
                pending, "sim, mas apague outra", "token"
            )

        self.assertIsNone(cleared)
        self.assertIn("não fiz nenhuma alteração", reply.casefold())
        backend.assert_not_awaited()

    async def test_backend_failure_does_not_claim_confirmation_succeeded(self):
        backend = AsyncMock(side_effect=main.BackendUnavailable("offline"))
        pending = {
            "kind": "delete_value",
            "args": {"id": 7},
            "description": "movimentação",
            "expires_at": main.monotonic() + 120,
        }
        with patch.object(main, "request_backend", backend):
            with self.assertRaises(main.BackendUnavailable):
                await main._responder_pendente(pending, "sim", "token")

        backend.assert_awaited_once_with("DELETE", "/valores/7", "token")

    def test_confirmation_parser_rejects_mixed_messages(self):
        self.assertEqual(main._classificar_confirmacao("SIM!"), "confirm")
        self.assertEqual(main._classificar_confirmacao("não"), "cancel")
        self.assertIsNone(main._classificar_confirmacao("sim, mas muda a data"))

    def test_confirmation_keys_are_isolated_by_token_and_conversation(self):
        payload = main.ChatRequest(input=[
            main.MessageItem(id="conversation-a", sender="user", content="Oi"),
        ])
        other_conversation = main.ChatRequest(input=[
            main.MessageItem(id="conversation-b", sender="user", content="Oi"),
        ])
        self.assertNotEqual(
            main._conversation_key(payload, "token-a"),
            main._conversation_key(payload, "token-b"),
        )
        self.assertNotEqual(
            main._conversation_key(payload, "token-a"),
            main._conversation_key(other_conversation, "token-a"),
        )

    async def test_pending_store_isolated_between_users(self):
        first_payload = main.ChatRequest(input=[
            main.MessageItem(id="conversation-a", sender="user", content="Oi"),
        ])
        second_payload = main.ChatRequest(input=[
            main.MessageItem(id="conversation-a", sender="user", content="Oi"),
        ])
        first_key = main._conversation_key(first_payload, "token-a")
        second_key = main._conversation_key(second_payload, "token-b")
        first_action = {"kind": "delete_value", "args": {"id": 7}, "expires_at": main.monotonic() + 120}
        second_action = {"kind": "delete_value", "args": {"id": 8}, "expires_at": main.monotonic() + 120}

        main._store_pending_action(first_key, first_action)
        main._store_pending_action(second_key, second_action)

        self.assertEqual(main._take_pending_action(first_key), first_action)
        self.assertEqual(main._take_pending_action(second_key), second_action)


if __name__ == "__main__":
    unittest.main()