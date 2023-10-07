import React from 'react';
import styles from './styles';
import { View, Text} from 'react-native';
import { Ionicons, AntDesign } from '@expo/vector-icons';

const Tutorial = () => {
    return ( 
            <View style={styles.border}>
                <View style={styles.box}>
                    <Ionicons name="ios-location-sharp" size={20} color="lightgreen" style={{left:10}} />
                    <Text style={styles.text}>
                        Informe seu local
                    </Text>
                </View>

                <View style={styles.box}>
                    <Ionicons name="add" size={20} color="lightgreen" style={{left:10}}/>
                    <Text style={styles.text}>
                        Busque e adicione seus produtos
                    </Text>
                </View>

                <View style={styles.box}>
                    <AntDesign name="bars" size={20} color="lightgreen" style={{left:10}}/>
                    <Text style={styles.text}>
                        Vá para sua lista de compras
                    </Text>
                </View>

                <View style={styles.box}>
                    <AntDesign name="star" size={20} color="lightgreen" style={{left:10}}/>
                    <Text style={styles.text}>
                        Veja as melhores opções
                    </Text>
                </View>

            </View>
    );
}

export default Tutorial;

