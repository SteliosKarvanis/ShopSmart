import React from 'react';
import styles from './styles';
import { View, Text, Pressable} from 'react-native';
import { Ionicons,  MaterialIcons, AntDesign  } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const OptionsScreen = () => {
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
        
        <View style={styles.border2}>
            <Text style={styles.title}> 
                Melhores Opções
            </Text>
        </View>


        <Pressable style={styles.buttonBackToList} onPress={() => navigation.navigate('ListScreen')}>
        <Text style={styles.text}>Voltar para lista</Text>
        </Pressable>

     
       
    </View>
    );
  };

export default OptionsScreen;