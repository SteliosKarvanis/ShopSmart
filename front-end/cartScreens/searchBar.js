import React, { useState,useEffect} from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView  } from 'react-native';
import styles from '../styles';
import Icon from 'react-native-vector-icons/FontAwesome'
import { Ionicons } from '@expo/vector-icons';
import Tutorial from './tutorial';
import { useGlobalContext } from '../context/context';
import { useGlobalContextLoc } from '../context/locationContext';


function SearchBarWithOptions() {
  const [searchText, setSearchText] = useState('');
  const [options, setOptions] = useState([]);
  const [showList, setShowList] = useState(false);
  // Simulated list of options for demonstration
  const { list, addElement,removeElement } = useGlobalContext();
  const {location,getCurrentLocation} = useGlobalContextLoc();


  // Function to filter options based on search text
  const filterOptions = (text) => {
    console.log(text)
    console.log(text.length)
    if (text.length > 0) {
      const apiBody = {'userSearch':text};
      const apiUrl = 'http://127.0.0.1:5000/server/search-product-type';
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiBody),
      })
        .then((response) => response.json())
        .then((data) => {
          setOptions(data.productList);
          setShowList(true);
        })
        .catch((error) => {
          console.error(error);
        });
        console.log(text)
      
    } else {
      setShowList(false);
      return;
    }
    
  };
  
  const handleSearch = (text) => {

    setSearchText(text);
    filterOptions(text);
  };

  return (
    <View >
      <View style={styles.searchbar}>

        <Icon name="search" size={20} color="black" style={styles.lupa} /> 
        <TextInput
          style={styles.textsearchbar}
          placeholder="Busque"
          onChangeText={handleSearch}
          onSubmitEditing={()=>setShowList(true)}
          value={searchText}
        />
        <TouchableOpacity style={styles.plus} onPress={getCurrentLocation}>
          <Ionicons name="ios-location-sharp" size={20} color="black" />
        </TouchableOpacity>

      </View>
      {!showList ? <Tutorial /> :
          <View style={{ height: 390 }}>
          <FlatList
              data={options}
              renderItem={({ item }) => (
                <View style={styles.option}>
                  <Text style={{fontSize: 13}}>
                    {item.name}
                  </Text>

                  <TouchableOpacity style={styles.plus} onPress={() => addElement(item)}>
                    <Ionicons name="add-circle-outline" size={20} color="black" />
                  </TouchableOpacity>
                </View>
              )}
              style={{ height: 410, overflow: 'scroll' }}
              keyExtractor={(item) => item}
            />
          </View>
      }
    </View>
  );
};

export default SearchBarWithOptions;
