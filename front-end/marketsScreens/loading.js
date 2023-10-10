import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import styles from '../styles';

const LoadingScreen = () => {
  return (
    <View style={styles.loading}>
      <Text>Carregando...</Text>
      <ActivityIndicator size="large" color="lightgreen" />
    </View>
  );
};

export default LoadingScreen;
