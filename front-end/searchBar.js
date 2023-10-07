import React, { useState } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView } from 'react-native';
import styles from './styles';
import Icon from 'react-native-vector-icons/FontAwesome'

const SearchBarWithOptions = () => {
  const [searchText, setSearchText] = useState('');
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [validOptions, setValidOptions] = useState([]);

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
    const filteredOptions = allOptions.filter((option) =>
      option.toLowerCase().includes(text.toLowerCase())
    );
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
      setValidOptions([...validOptions, searchText]);
      setSearchText('');
    }
  };
  console.log(allOptions.length);
  return (
    <View>
        <View style={styles.searchbar}>
            <Icon name="search" size={20} color="black" style={{}} /> {/* Ícone de lupa */}
            <TextInput
                style={styles.textsearchbar}
                placeholder="Busque"
                onChangeText={handleSearch}
                onKeyPress={handleKeyPress}
                value={searchText}
            />
        </View>
      <ScrollView>
        {validOptions.map((option) => (
          <View key={option} style={{ padding: 20, margin: 5 }}>
            {options.length > 0 && (
            <FlatList
                data={options}
                renderItem={({ item }) => (
                    <TouchableOpacity onPress={() => handleOptionSelect(item)}>
                        <Text style={styles.option}>{item}</Text>
                    </TouchableOpacity>
                )}
                keyExtractor={(item) => item}
            />
            )}
            {selectedOption && (
                <Text>Selected Option: {selectedOption}</Text>
            )}
          </View>
        ))}
      </ScrollView>
      
    </View>
  );
};

export default SearchBarWithOptions;
