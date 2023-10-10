import React, { useState, useEffect } from 'react';
import styles from '../styles';
import { View, Text, Pressable} from 'react-native';
import { Ionicons,  MaterialIcons, AntDesign  } from '@expo/vector-icons';
import { useNavigation} from '@react-navigation/native';
import Title from '../title';
import LoadingScreen from './loading';
import Tutorial from '../cartScreens/tutorial';

const MarketsScreen = () => {
    const navigation = useNavigation();
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        setTimeout(() => {
          setIsLoading(false);
        }, 3000);
      }, []);
    return (
    <View style={styles.container}>
        <Title/>
        
        <View style = {styles.bestMarketsBox}>
            <Text style={styles.bestMarkets}> 
                Melhores Mercados
            </Text>
            <Ionicons name="star" size={20} color="black" style={{ position: 'absolute', right: 10 }} />
        </View>
        {
            isLoading? <LoadingScreen/>: <Tutorial/>
        }


        <Pressable style={styles.buttonBackToList} onPress={() => navigation.navigate('ListScreen')}>
            <Ionicons name="ios-arrow-back" size={30} color="black" />
            <Text style={styles.text}>Voltar para lista</Text>
        </Pressable>

     
       
    </View>
    );
  };

export default MarketsScreen;