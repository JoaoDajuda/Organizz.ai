import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Login from './pages/login/Login'
import Financas from './pages/financas/Financas'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* <Login /> */}
    <Financas/>
  </StrictMode>,
)
