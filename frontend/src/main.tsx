import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { MantineProvider, Text } from '@mantine/core';


const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
  <MantineProvider>
    <App />
  </MantineProvider>

)
