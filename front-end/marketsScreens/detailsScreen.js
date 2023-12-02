import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView ,Pressable } from 'react-native';
import styles from '../styles';
import { Ionicons,  MaterialIcons, AntDesign  } from '@expo/vector-icons';
import { useNavigation} from '@react-navigation/native';
import Title from '../title';
import LoadingScreen from './loading';

const DetailsScreen = () => {
    const navigation = useNavigation();

    return <View style={styles.container}>
        <Title/>
        <Pressable style={styles.buttonBackToList} onPress={() => navigation.navigate('MarketsScreen')}>
            <Ionicons name="ios-arrow-back" size={30} color="black" />
            <Text style={styles.text}>Voltar para mercados</Text>
        </Pressable>
    </View>
  };

export default DetailsScreen;