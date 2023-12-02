import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, Text, TouchableOpacity, Keyboard, ScrollView, Pressable } from 'react-native';
import styles from '../styles';
import { Ionicons, MaterialIcons, AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import Title from '../title';
import LoadingScreen from './loading';

const MarketsScreen = () => {
  const navigation = useNavigation();
  const data = {
    "Markets": [
      {
        "name": "Carrefour",
        "distance": 4.3,
        "total": 24,
        "cartInstances": [
          {
            "name": "Toddinho 200 ml",
            "qte": 2,
            "unityPrice": 20,
            "subtotal": 10
          },
          {
            "name": "Barra garoto 200g",
            "qte": 3,
            "unityPrice": 20,
            "subtotal": 14
          }
        ]
      },
      {
        "name": "Esperanca",
        "distance": 5.8,
        "total": 18,
        "cartInstances": [
          {
            "name": "Toddinho 200 ml",
            "qte": 5,
            "unityPrice": 20,
            "subtotal": 8
          },
          {
            "name": "Barra Alpino 100g",
            "qte": 8,
            "unityPrice": 20,
            "subtotal": 10
          }
        ]
      },
      {
        "name": "Esperanca",
        "distance": 5.8,
        "total": 18,
        "cartInstances": [
          {
            "name": "Toddinho 200 ml",
            "qte": 5,
            "unityPrice": 20,
            "subtotal": 8
          },
          {
            "name": "Barra Alpino 100g",
            "qte": 8,
            "unityPrice": 20,
            "subtotal": 10
          }
        ]
      },
      {
        "name": "Esperanca",
        "distance": 5.8,
        "total": 18,
        "cartInstances": [
          {
            "name": "Toddinho 200 ml",
            "qte": 5,
            "unityPrice": 20,
            "subtotal": 8
          },
          {
            "name": "Barra Alpino 100g",
            "qte": 8,
            "unityPrice": 20,
            "subtotal": 10
          }
        ]
      },
      {
        "name": "Esperanca",
        "distance": 5.8,
        "total": 18,
        "cartInstances": [
          {
            "name": "Toddinho 200 ml",
            "qte": 5,
            "unityPrice": 20,
            "subtotal": 8
          },
          {
            "name": "Barra Alpino 100g",
            "qte": 8,
            "unityPrice": 20,
            "subtotal": 10
          }
        ]
      },
      {
        "name": "Esperanca",
        "distance": 5.8,
        "total": 18,
        "cartInstances": [
          {
            "name": "Toddinho 200 ml",
            "qte": 5,
            "unityPrice": 20,
            "subtotal": 8
          },
          {
            "name": "Barra Alpino 100g",
            "qte": 8,
            "unityPrice": 20,
            "subtotal": 10
          }
        ]
      }
    ]
  }
  const [detail, SetDetail] = useState([]);
  console.log(detail)
  const handleDetail= (det) => {
    SetDetail(det);
  };
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
              data={data.Markets}
              renderItem={({ item }) => (
                <View style={styles.option2}>
                  <Text style={{ flex: 1, flexDirection: 'col', left: 80 }}>
                    {item.name}

                  </Text>
                  <Text style={{ flex: 1, flexDirection: 'col', left: 80 }}>
                    {item.distance} km
                  </Text>
                  <Text style={{ right: 50, position: 'absolute', fontSize: 20 }}>
                    R$ {item.total}
                  </Text>

                  <TouchableOpacity style={styles.plus} onPress={() => {navigation.navigate('DetailsScreen');
                                                                        handleDetail(item);}}>
                    <AntDesign name="rightcircleo" size={20} color="black" />
                  </TouchableOpacity>
                </View>
              )}
              style={{ height: 300, overflow: 'scroll', top: 120 }}
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