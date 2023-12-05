import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView, Pressable } from 'react-native';
import styles from '../styles';
import { Ionicons, MaterialIcons, AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import Title from '../title';
import LoadingScreen from './loading';
import { useDetailContext } from '../context/detailContext';
import { useMarketContext } from '../context/marketContext';

const MarketsScreen = () => {
  const navigation = useNavigation();
  const { detail, handleDetail } = useDetailContext();
  const { markets, handleMarket } = useMarketContext();
  console.log(markets);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  }, []);
  return (
    <View style={styles.container}>
      <Title />

      <View style={styles.bestMarketsBox}>
        <Text style={styles.bestMarkets}>
          Melhores Mercados
        </Text>
        <Ionicons name="star" size={20} color="black" style={{ position: 'absolute', right: 10 }} />
      </View >
      {
        isLoading ? <LoadingScreen /> :
          <View style={{ height: 340 }}>
            <FlatList
              data={markets}
              renderItem={({ item }) => (
                <View style={styles.option2}>
                <View style={{ flex: 1, flexDirection: 'col', left: 20 }}>
                <Text style={{ flexWrap: 'wrap' }}>
                  {item.name}
                </Text>
                <Text style={{ flexWrap: 'wrap' }}>
                {item.distance} km
                </Text>
                {item.missing ?
                    <Text style={{ flexWrap: 'wrap', color: 'red' }}>
                        Item faltando!
                    </Text> : null}
              </View>
                  

                  <Text style={{ right: 20, display: 'flex', fontSize: 15, color: 'green' }}>
                    R$ {item.total}
                  </Text>

                  <TouchableOpacity style={styles.plus} onPress={() => {
                    navigation.navigate('DetailsScreen');
                    handleDetail(item);
                  }}>
                    <AntDesign name="rightcircleo" size={20} color="black" />
                  </TouchableOpacity>
                </View>
              )}
              style={{ height: 350, overflow: 'scroll', top: 120 }}
              keyExtractor={(item) => item}
            />
          </View>
      }


      <Pressable style={styles.buttonBackToList} onPress={() => navigation.navigate('ListScreen')}>
        <Ionicons name="ios-arrow-back" size={30} color="black" />
        <Text style={styles.text}>Voltar para lista</Text>
      </Pressable>



    </View>
  );
};

export default MarketsScreen;