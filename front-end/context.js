import React, { createContext, useContext, useState } from 'react';
const GlobalContext = createContext();

export const useGlobalContext = () => useContext(GlobalContext);

export const GlobalProvider = ({ children }) => {
  const [list, setList] = useState([]);

  function toggleSelection(option){
    if (!list.includes(option)) {
        setList([...list, option]);
    } 
  };
  return (
    <GlobalContext.Provider value={{ list,toggleSelection }}>
      {children}
    </GlobalContext.Provider>
  );
};
