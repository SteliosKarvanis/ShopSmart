import React, { createContext, useContext, useState } from 'react';
const DetailContext = createContext();

export const useDetailContext = () => useContext(DetailContext);

export const DetailProvider = ({ children }) => {
  const [detail, setDetail] = useState([]);
  console.log(detail)
  const handleDetail= (det) => {
    setDetail(det);
  };
  
  return (
    <DetailContext.Provider value={{ detail, handleDetail }}>
      {children}
    </DetailContext.Provider>
  );
};
