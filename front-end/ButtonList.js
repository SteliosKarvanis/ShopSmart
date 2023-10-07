import React from 'react';
import styles from './styles';
import { Text, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const ButtonList = ({ navigation }) => {
  return (
    <Pressable
      style={styles.buttonToOptions}
      onPress={() => navigation.navigate('OptionsScreen')}
    >
      <Text style={styles.text}>Quero comprar barato</Text>
      <Ionicons name="star" size={20} color="black" />
    </Pressable>
  );
};

export default ButtonList;
