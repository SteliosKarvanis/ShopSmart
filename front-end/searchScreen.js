import React from 'react';
import styles from './styles';
import { View, TextInput, Text, StyleSheet, Button,Pressable } from 'react-native';
import { Ionicons,  MaterialIcons, AntDesign  } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const SearchScreen = () => {
    const navigation = useNavigation();
    return (
      <View style={styles.container}>
  
        <View style={styles.titleBox}>
          <MaterialIcons name="shopping-cart" size={80} color="lightgreen" />
            <View style={styles.titleText}>
                <Text style={styles.title}> 
                     ShopSmart
                </Text>
                <Text style={styles.subtitle}>     
                    Comprando com sabedoria
                </Text>
            </View>
        </View>
  
        <View style={styles.border}>
            <View style={styles.box}>
                <Ionicons name="ios-location-sharp" size={20} color="lightgreen" />
                <Text style={styles.text}>
                     Informe seu local 
                </Text>
            </View>
            
            <View style={styles.box}>
                <Ionicons name="add" size={20} color="lightgreen" />
                <Text style={styles.text}>
                     Busque e adicione seus produtos
                </Text>
            </View>
  
            <View style={styles.box}>
                <AntDesign name="bars" size={20} color="lightgreen" />
                <Text style={styles.text}>
                     Vá para sua lista de compras
                </Text>
            </View>
            
            <View style={styles.box}>
                <AntDesign name="star" size={20} color="lightgreen" />
                <Text style={styles.text}>
                    Veja as melhores opções
                </Text>
            </View>
         </View>
        
        <input type='text' style={styles.searchbar}/>
  
        <View style={styles.buttonBoxLeft1}>
                <Ionicons name="search" size={20} color="black" />
                <Text style={styles.text}>
                    Busca
                </Text>
        </View>
  
                
        <Pressable style={styles.buttonBoxRight1} onPress={() => navigation.navigate('ListScreen')}>
        <AntDesign name="bars" size={20} color="black" />
            <Text style={styles.text}>Lista</Text>
            </Pressable>
        
         
      </View>
    );
};

export default SearchScreen;