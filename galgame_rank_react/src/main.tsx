import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Home from './routes/Home'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryCLient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryCLient}>
      <Home />
    </QueryClientProvider>
  </StrictMode>,
)
