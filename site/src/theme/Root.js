import React from 'react';
import ChatbotWidget from '../components/ChatbotWidget';

const Root = ({ children }) => {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
};

export default Root;