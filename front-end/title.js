import React from 'react';
import { View, Image } from 'react-native';

const Title = () => {
    return (
        <View>
            <Image
                source={require('./assets/title.png')}
                style={{ width: 400, height: 100, top:10, resizeMode: 'contain'}}
            />

        </View>
    );
}

export default Title;

