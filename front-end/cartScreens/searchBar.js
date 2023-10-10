import React, { useState} from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView } from 'react-native';
import styles from '../styles';
import Icon from 'react-native-vector-icons/FontAwesome'
import { Ionicons } from '@expo/vector-icons';
import Tutorial from './tutorial';
import { useGlobalContext } from '../context';

function SearchBarWithOptions() {
  const [searchText, setSearchText] = useState('');
  const [options, setOptions] = useState([]);
  const [showList, setShowList] = useState(false);
  // Simulated list of options for demonstration
  const { list, addElement,removeElement } = useGlobalContext();
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
  ];

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


  const handleKeyPress = (e) => {
    if (e.nativeEvent.key === 'Enter') {
      // Handle Enter key press here
      Keyboard.dismiss(); // Dismiss the keyboard
      setShowList(true);
    }
  };

  {/* <Text>Selected Options:</Text>
          {list.length>0 && list.map((selectedOption) => (
            <Text key={selectedOption}>{selectedOption}</Text>
          ))} */}

  return (
    <View >
      <View style={styles.searchbar}>

        <Icon name="search" size={20} color="black" style={styles.lupa} /> {/* Ícone de lupa */}
        <TextInput
          style={styles.textsearchbar}
          placeholder="Busque"
          onChangeText={handleSearch}
          onKeyPress={handleKeyPress}
          value={searchText}
        />
        <TouchableOpacity style={styles.plus} onPress={() => (null)}>
          <Ionicons name="ios-location-sharp" size={20} color="black" />
        </TouchableOpacity>

      </View>
      {!showList ? <Tutorial /> :

        <ScrollView>
          {
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
              style={{ height: 200, overflow: 'scroll' }}
              keyExtractor={(item) => item}
            />}



        </ScrollView>
      }
    </View>
  );
};

export default SearchBarWithOptions;
