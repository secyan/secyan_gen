import React from 'react';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
import { CodeProvider } from './components/model/CodeContext';
import HomePage from './components/pages/home/HomePage';

function App() {
  return (
    <CodeProvider>
      <HomePage />
    </CodeProvider>
  );
}

export default App;
