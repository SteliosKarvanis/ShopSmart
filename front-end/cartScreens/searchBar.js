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
  const allOptions = [
    'Apple',
    'Banana',
    'Bolo',
    'Cherry',
    'Date',
    'Grape',
    'Lemon',
    'Mango',
    'Orange',
    'Pineapple',
    'Strawberry',
    'Watermelon',
    'a',
    'aa',
    'aaa',
    'aaaaa',
    'aaaaaaa'
  ];

  // Location
  

  // Function to filter options based on search text
  const filterOptions = (text) => {
    const filteredOptions = allOptions.filter((option) => {
      if (text !== '')
        return option.toLowerCase().includes(text.toLowerCase()) 
      else {
        setShowList(false)
        return ''
      }
    });
    setOptions(filteredOptions);
  };

  const handleSearch = (text) => {

    setSearchText(text);
    filterOptions(text);
  };
  console.log(location)

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
                    {item}
                  </Text>
                  <TouchableOpacity style={styles.plus} onPress={() => addElement(item)}>
                    <Ionicons name="add" size={20} color="black" />
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
