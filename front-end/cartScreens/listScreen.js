import React from 'react';
import styles from '../styles';
import { View, Text, Pressable, FlatList, TouchableOpacity, ScrollView } from 'react-native';
import { Ionicons, MaterialIcons, AntDesign } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import Title from '../title';
import { useGlobalContext } from '../context/context';
import { useMarketContext } from '../context/marketContext';	
import { useGlobalContextLoc } from '../context/locationContext';

function ListScreen() {
  const navigation = useNavigation();
  const {location,getCurrentLocation} = useGlobalContextLoc();
  const { list, addElement, removeElement } = useGlobalContext();
  const { market, handleMarket } = useMarketContext();
  return (
    <View style={styles.container}>
      <Title />

      <View style={{ height: 390 }}>
        <FlatList
          data={list}
          renderItem={({ item }) => (
            <View style={styles.option}>
              <Text >
                {item.unities} X {item.name}
              </Text>
              <TouchableOpacity style={styles.plus} onPress={() => removeElement(item)}>
                <Ionicons name="remove-circle-outline" size={20} color="black" />
              </TouchableOpacity>
            </View>
          )}
          style={{ height: 430, overflow: 'scroll' }}
          keyExtractor={(item) => item}
        />
      </View>



      <View style={styles.buttonBoxRight2}>
        <AntDesign name="bars" size={20} color="black" />

        <Text >
          Lista
        </Text>
      </View>

      <Pressable style={styles.buttonBoxLeft2} onPress={() => navigation.navigate('Home')}>
        <Ionicons name="search" size={20} color="black" />
        <Text >Busca</Text>
      </Pressable>


      <TouchableOpacity
        style={styles.buttonToOptions}
        onPress={() => {
          navigation.navigate('MarketsScreen');
          handleMarket(list,location);
        }}
      >
        <Text style={styles.text}>Quero comprar barato</Text>
        <Ionicons name="star" size={20} color="black" style={{ position: 'absolute', right: 10 }} />
      </TouchableOpacity>


    </View>
  );
};

export default ListScreen;