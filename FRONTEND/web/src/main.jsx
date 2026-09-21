import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider, Navigate } from "react-router-dom"
import Header from "./components/Header/Header.jsx"
import Calendar from "./components/Calendar/Calendar.jsx"
import Login from "./pages/login/Login.jsx"
import Rotina from "./pages/rotina/Rotina.jsx"
import Financas from "./pages/financas/Financas.jsx"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/login" replace />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/app",
    element: <Header />,
    children: [
      { index: true, element: <Navigate to="rotina" replace /> },
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