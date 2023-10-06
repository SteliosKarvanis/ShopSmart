import SearchScreen from './searchScreen';
import ListScreen from './listScreen';
import OptionsScreen from './optionsScreen';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';


const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={SearchScreen} options={{ headerShown: false }}/>
        <Stack.Screen name="ListScreen" component={ListScreen} options={{ headerShown: false }}/>
        <Stack.Screen name="OptionsScreen" component={OptionsScreen} options={{ headerShown: false }}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;

