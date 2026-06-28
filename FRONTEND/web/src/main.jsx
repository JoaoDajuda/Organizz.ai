import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Login from './pages/Login'
import Financas from './pages/Financas'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Financas />
  </StrictMode>,
)
