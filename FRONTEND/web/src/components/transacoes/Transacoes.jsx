export default function Transacoes(dadosTransacoes) {
    return (
        <div>
            {dadosTransacoes.map((transacao, index) => (
                <div key={index}>
                    <p>{transacao.descricao}</p>
                    <p>R$ {transacao.valor.toFixed(2)}</p>
                </div>
            ))}
        </div>
    )
}