import React, { createContext, useContext, useState } from 'react';
const MarketContext = createContext();

export const useMarketContext = () => useContext(MarketContext);

export const MarketProvider = ({ children }) => {
    const [markets, setMarket] = useState([]);
    console.log(markets)
    const handleMarket =(list, location) => {
        const apiBody = {
            "userLocation": {
                "lat": location.latitude,
                "lon": location.longitude
            },
            "productList": list,
            "maxDistance": 10
        };
        const apiUrl = 'http://127.0.0.1:5000/server/recommend-markets';
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(apiBody),
        })
            .then((response) => response.json())
            .then((data) => {
                setMarket(data.Markets);
            })
        console.log(markets)
    };
    return (
        <MarketContext.Provider value={{ markets, handleMarket }}>
            {children}
        </MarketContext.Provider>
    );
};
