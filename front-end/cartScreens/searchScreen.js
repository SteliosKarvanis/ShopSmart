import React, { useState } from 'react';
import styles from '../styles';
import SearchBarWithOptions from './searchBar';
import { View, TextInput, Text, StyleSheet, Button, Pressable } from 'react-native';
import { Ionicons, MaterialIcons, AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import Title from '../title';

const SearchScreen = () => {
    const navigation = useNavigation();
    return (
        <View style={styles.container}>

            <Title />

            <SearchBarWithOptions/> {/* Render the SearchBarWithOptions component */}
            
            <View style={styles.buttonBoxLeft1}>
                <Ionicons name="search" size={20} color="black" />
                <Text>
                    Busca
                </Text>
            </View>


            <Pressable style={styles.buttonBoxRight1} onPress={() => navigation.navigate('ListScreen')}>
                <AntDesign name="bars" size={20} color="black" />
                <Text >Lista</Text>
            </Pressable>


        </View>
    );
};

export default SearchScreen;