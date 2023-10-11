import React, { createContext, useContext, useState } from 'react';
const GlobalContext = createContext();

export const useGlobalContext = () => useContext(GlobalContext);

export const GlobalProvider = ({ children }) => {
  const [list, setList] = useState([]);
  
  function addElement(option){
    if (!list.includes(option)) {
        setList([...list, option]);
    } 
  };

  function removeElement(option){
    if (list.includes(option)) {
        setList(list.filter(item => item !== option));
    } 
  };
  return (
    <GlobalContext.Provider value={{ list,addElement,removeElement }}>
      {children}
    </GlobalContext.Provider>
  );
};
