import RouterDOM from 'react-dom/client'
import { BrowserRouter,Routes,Route } from 'react-router'
import './index.css'
import Home from './pages/Home'
import Project from './pages/Project'

RouterDOM.createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/project/:projectId" element={<Project />} />
    </Routes>
  </BrowserRouter>,
)
