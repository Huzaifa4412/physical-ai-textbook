import React, { lazy, Suspense } from 'react';

const ChatbotWidget = lazy(() => import('../components/ChatbotWidget'));

const Root = ({ children }) => {
  return (
    <>
      {children}
      <Suspense fallback={null}>
        <ChatbotWidget />
      </Suspense>
    </>
  );
};

export default Root;