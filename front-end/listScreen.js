import React from 'react';
import styles from './styles';
import { View, TextInput, Text, StyleSheet, Button, Pressable} from 'react-native';
import { Ionicons,  MaterialIcons, AntDesign  } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import ButtonList from './ButtonList';

const ListScreen = () => {
    const navigation = useNavigation();
    return (
    <View style={styles.container}>
        <View style={styles.titleBox}>
            <MaterialIcons name="shopping-cart" size={80} color="lightgreen"/>
                <View style={styles.titleText}>
                    <Text style={styles.title}> 
                        ShopSmart
                    </Text>
                    <Text style={styles.subtitle}>     
                        Comprando com sabedoria
                    </Text>
                </View>
        </View>
        
        <View style={styles.border2}>
            <Text style={styles.title}> 
                        Minha Lista
                    </Text>
        </View>

        <View style={styles.buttonBoxRight2}>
                <AntDesign name="bars" size={20} color="black" />
                
                <Text style={styles.text}>
                    Lista
                </Text>
        </View>
    
        <Pressable style={styles.buttonBoxLeft2} onPress={() => navigation.navigate('Home')}>
        <Ionicons name="search" size={20} color="black" />
        <Text style={styles.text}>Busca</Text>
        </Pressable>

        
        <ButtonList />
     
       
    </View>
    );
  };

export default ListScreen;