import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView ,Pressable } from 'react-native';
import styles from '../styles';
import { Ionicons,  MaterialIcons, AntDesign  } from '@expo/vector-icons';
import { useNavigation} from '@react-navigation/native';
import Title from '../title';
import { useDetailContext } from '../detailContext';

const DetailsScreen = () => {
    const navigation = useNavigation();
    const { detail, handleDetail } = useDetailContext();
    return (
        <View style={styles.container}>
          <Title />
    
          <View style={styles.bestMarketsBox}>
            <Text style={styles.bestMarkets}>
              {detail.name}     
            </Text>
            <Text style={{right:20, position: 'absolute', fontSize: 30}}>
              R$ {detail.total}     
            </Text>
          </View >
          
              <View style={{ height: 340 }}>
                <FlatList
                  data={detail.cartInstances}
                  renderItem={({ item }) => (
                    <View style={styles.option2}>
                      <Text style={{ flex: 1, flexDirection: 'col', left: 80 }}>
                        {item.name}
    
                      </Text>
                      <Text style={{ flex: 1, flexDirection: 'col', left: 80 }}>
                        Quantidade: {item.qte} 
                      </Text>
                      <Text style={{ flex: 1, flexDirection: 'col', left: 80 }}>
                        Preço unitário: R$ {item.unityPrice} 
                      </Text>
                      <Text style={{ right: 30, position: 'absolute', fontSize: 20 }}>
                        R$ {item.subtotal}
                      </Text> 
                    </View>
                  )}
                  style={{ height: 350, overflow: 'scroll', top: 120 }}
                  keyExtractor={(item) => item}
                />
              </View>
    

          <Pressable style={styles.buttonBackToList} onPress={() => navigation.navigate('MarketsScreen')}>
            <Ionicons name="ios-arrow-back" size={30} color="black" />
            <Text style={styles.text}>Voltar para mercados</Text>
          </Pressable>
    
            
    
        </View>
      );
 };

export default DetailsScreen;