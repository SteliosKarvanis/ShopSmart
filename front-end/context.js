import React, { createContext, useContext, useState } from 'react';
const GlobalContext = createContext();

export const useGlobalContext = () => useContext(GlobalContext);

export const GlobalProvider = ({ children }) => {
  const [list, setList] = useState([]);
  
  function addElement(option){
    if (list.some(item => item.name === option.name)) {
      setList(
        list.map((item) =>
          item.name === option.name ? { ...item, unities: item.unities + 1 } : item
        )
      );
        
    } else {
      setList([...list, option]);
    }
  };

  function removeElement(option){
    if (list.includes(option)) {
        if (option.unities === 1) {
          setList(list.filter(item => item !== option));
        } else {
          setList(
            list.map((item) =>
              item === option ? { ...item, unities: item.unities - 1 } : item)
            )
        }
    } 
  };
  return (
    <GlobalContext.Provider value={{ list,addElement,removeElement }}>
      {children}
    </GlobalContext.Provider>
  );
};
