import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Login from './pages/login/Login.jsx'
import Financas from './pages/financas/Financas.jsx'
import Rotina from './pages/rotina/Rotina.jsx'
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import Header from "./components/Header/Header.jsx"
import Calendar from "./components/Calendar/Calendar.jsx"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Header />,
    children: [
      { index: true, element: <Calendar /> },     // "/" → Início/Agenda
      { path: "rotina", element: <Rotina /> },
      { path: "financas", element: <Financas /> },
    ],
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)