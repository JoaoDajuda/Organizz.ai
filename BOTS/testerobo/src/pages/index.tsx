import React, { useState } from 'react';
import { SendHorizontal, Send, X, UserPen } from 'lucide-react';
import Modal from 'react-modal';
import './index.css';

const sendMensagem = async (messageHistory) => {
  try {
    const response = await fetch('http://localhost:8000/robo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: messageHistory }),
    });
    return await response.json();
  } catch (error) {
    console.error('Erro na requisição:', error);
  }
};

function Index() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      content: 'Olá, sou a Athena, sua assistente virtual focada em finanças. Qual seu nome e como posso te ajudar hoje?',
      type: 'markdown'
    }
  ]);
  const [open, setOpen] = useState(false);

  function Abrirmodal() {
    setOpen(!open);
  }

  const HandleSending = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      content: input,
      type: 'text'
    };

    const updateMessages = [...messages, userMessage];
    setMessages(updateMessages);
    setInput('');

    try {
      const resposta = await sendMensagem(updateMessages);

      if (resposta && resposta.reply) {
        const botMessage = {
          id: Date.now() + 1,
          sender: 'bot',
          content: resposta.reply,
          type: 'markdown'
        };
        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      console.error("Erro ao obter resposta do robô:", error);
    }
  };

  return (
    <>
      <SendHorizontal onClick={Abrirmodal} cursor='pointer' />
      <Modal isOpen={open} className='modal' ariaHideApp={false}>
        <X onClick={Abrirmodal} cursor='pointer' className='X' />
        
        <div className='msglist'>
          {messages.map((msg) => (
            <div key={msg.id} className={`msgitem ${msg.sender}`}>
                <UserPen />
                <strong>{msg.sender === 'bot' ? 'Athena' : 'Você'}: </strong>
                <p>{msg.content}</p>
            </div>
          ))}
        </div>

        <div className='padrao'>
          <input
            className='InputUser'
            type='text'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && HandleSending()}
            placeholder='Envie sua mensagem . . .'
          />
          <Send className='buttonsend' onClick={HandleSending} cursor='pointer' />
        </div>
      </Modal>
    </>
  );
}

export default Index;