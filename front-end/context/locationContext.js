import React, { createContext, useContext, useState, useEffect } from 'react';
import Geolocation from '@react-native-community/geolocation';

const GlobalContextLoc = createContext();

export const useGlobalContextLoc = () => useContext(GlobalContextLoc);

export const GlobalProviderLoc = ({ children }) => {
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(true);

  const getCurrentLocation = () => {
    Geolocation.getCurrentPosition(
      position => {
        setLocation(position.coords);
        setLoading(false);
      },
      error => {
        alert(error.message);
        setLoading(false);
      },
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
    );
  };

  useEffect(() => {
    getCurrentLocation(); // Get the location when the component mounts
  }, []);

  return (
    <GlobalContextLoc.Provider value={{ location, getCurrentLocation }}>
      {children}
    </GlobalContextLoc.Provider>
  );
};
