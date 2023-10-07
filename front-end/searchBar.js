import React, { useState, useMemo } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView } from 'react-native';
import styles from './styles';
import Icon from 'react-native-vector-icons/FontAwesome'
import { Ionicons, MaterialIcons, AntDesign } from '@expo/vector-icons';
import Tutorial from './tutorial';

const SearchBarWithOptions = () => {
  const [searchText, setSearchText] = useState('');
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [showList, setShowList] = useState(false);
  //const [validOptions, setValidOptions] = useState([]);

  // Simulated list of options for demonstration
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
      return text !== '' ? option.toLowerCase().includes(text.toLowerCase()) : ''
    });
    setOptions(filteredOptions);
  };

  const handleSearch = (text) => {

    setSearchText(text);
    filterOptions(text);
  };

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    setSearchText(option); // Set the selected option as the search text
  };

  const handleKeyPress = (e) => {
    if (e.nativeEvent.key === 'Enter') {
      // Handle Enter key press here
      Keyboard.dismiss(); // Dismiss the keyboard
      setShowList(true);
    }
  };

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
        <TouchableOpacity style={styles.plus} onPress={() => handleOptionSelect(item)}>
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
                  <TouchableOpacity style={styles.plus} onPress={() => handleOptionSelect(item)}>
                    <Ionicons name="add" size={20} color="black" />
                  </TouchableOpacity>
                </View>
              )}
              style={{ height: 200, overflow: 'scroll' }}
              keyExtractor={(item) => item}
            />}
          {selectedOption && (
            <Text>Selected Option: {selectedOption}</Text>
          )}


        </ScrollView>
      }
    </View>
  );
};

export default SearchBarWithOptions;
