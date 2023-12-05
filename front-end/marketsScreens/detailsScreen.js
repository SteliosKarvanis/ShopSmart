import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView, Pressable } from 'react-native';
import styles from '../styles';
import { Ionicons, MaterialIcons, AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import Title from '../title';
import { useDetailContext } from '../context/detailContext';

const DetailsScreen = () => {
  const navigation = useNavigation();
  const { detail, handleDetail } = useDetailContext();
  return (
    <View style={styles.container}>
      <Title />

      <View style={styles.bestMarketsBox}>
        <Text style={{
          left: 15,
          fontSize: 15,
          marginBottom: 0,
          flexWrap: 'wrap'
        }}>
          {detail.name}
        </Text>
        <Text style={{ right: 8, position:'absolute', fontSize: 15, color: 'green' }}>
          R$ {detail.total}
        </Text>
      </View >

      <View style={{ height: 340 }}>
        <FlatList
          data={detail.cartInstances}
          renderItem={({ item }) => (
            <View style={styles.option2}>

              <View style={{ flex: 1, flexDirection: 'col', left: 20 }}>
                <Text style={{ flexWrap: 'wrap' }}>
                  {item.name}
                </Text>
                <Text style={{ flexWrap: 'wrap' }}>
                  Quantidade: {item.qte}
                </Text>
                <Text style={{ flexWrap: 'wrap' }}>
                  Preço unitário: {item.unityPrice}
                </Text>
              </View>

              <Text style={{ right: 20, display: 'flex', fontSize: 15, color: 'green' }}>
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