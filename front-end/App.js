import SearchScreen from './cartScreens/searchScreen';
import ListScreen from './cartScreens/listScreen';
import DetailsScreen from './marketsScreens/detailsScreen';
import MarketsScreen from './marketsScreens/marketsScreen';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { GlobalProvider } from './context';
import { GlobalProviderLoc } from './locationContext';
import { DetailProvider } from './detailContext';

const Stack = createStackNavigator();

function App() {
  return (
    <DetailProvider>
      <GlobalProviderLoc>
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
              <Stack.Screen
                name="DetailsScreen"
                component={DetailsScreen}
                options={{ headerShown: false }}
              />
            </Stack.Navigator>
          </NavigationContainer>
        </GlobalProvider>
      </GlobalProviderLoc>
    </DetailProvider>

  );
}

export default App;


