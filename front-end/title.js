import React from 'react';
import styles from './styles';
import { Text, View } from 'react-native';
import {MaterialIcons} from '@expo/vector-icons';

const Title = () => {
    return (
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
    );
}

export default Title;

