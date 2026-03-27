import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import App from './App.tsx'
import { A40Blog } from './blog/A40Blog.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/a40" element={<A40Blog />} />
        <Route path="/a40/:slug" element={<A40Blog />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
