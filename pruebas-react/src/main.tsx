import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BlogApp } from './BlogApi'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BlogApp></BlogApp>
  </StrictMode>,
)
