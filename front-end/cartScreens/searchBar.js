import React, { useState,useEffect} from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView  } from 'react-native';
import styles from '../styles';
import Icon from 'react-native-vector-icons/FontAwesome'
import { Ionicons } from '@expo/vector-icons';
import Tutorial from './tutorial';
import { useGlobalContext } from '../context';
import { useGlobalContextLoc } from '../locationContext';


function SearchBarWithOptions() {
  const [searchText, setSearchText] = useState('');
  const [options, setOptions] = useState([]);
  const [showList, setShowList] = useState(false);
  // Simulated list of options for demonstration
  const { list, addElement,removeElement } = useGlobalContext();
  const {location,getCurrentLocation} = useGlobalContextLoc();
  const data = {
    "productList":[
            {
                "name":"Achocolatado",
                "imageSampleUrl": "acho.png",
                "unity":"ml",
                "qtd":200,
                "unities":1
            },
            {
                "name":"Chocolate",
                "imageSampleUrl": "choco.png",
                "unity":"grams",
                "qtd":175,
                "unities":1
            }
        ]
}



  // Function to filter options based on search text
  const filterOptions = (text) => {
    const filteredOptions = data.productList.filter((product) => {
      if (text !== '' && product.name.toLowerCase().includes(text.toLowerCase()))
          return product
      else {
        setShowList(false)
        return null
      }
    })
    setOptions(filteredOptions);
  };
  
  const handleSearch = (text) => {

    setSearchText(text);
    filterOptions(text);
  };
  console.log(list)

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
                  <Text >
                    {item.name} {item.qtd} {item.unity}
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
