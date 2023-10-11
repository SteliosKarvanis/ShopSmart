import SearchScreen from './cartScreens/searchScreen';
import ListScreen from './cartScreens/listScreen';
import MarketsScreen from './marketsScreens/marketsScreen';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { GlobalProvider } from './context';

const Stack = createStackNavigator();

function App() {
  return (
    <GlobalProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen
            name="Home"
            component={SearchScreen}
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="ListScreen"
            component={ListScreen}
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="MarketsScreen"
            component={MarketsScreen}
            options={{ headerShown: false }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </GlobalProvider>

  );
}

export default App;


