const styles = {
    loading: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    bestMarkets: {
      left:15,
      fontSize: 30,
      marginBottom: 0,
    },
    bestMarketsBox:{
      position: 'absolute',
      top: 150,
      width: '100%',
      flexDirection: 'row',
      alignItems: 'center',
      borderWidth: 1,
      backgroundColor: 'lightgreen',
      borderRadius: 10,
      height: 50,
      width: 330,
    },
    lupa: {
      position: 'absolute',
      left: 10
    },
    plus: {
      backgroundColor: 'lightgrey',
      position: 'absolute',
      right: 10
    },
    option: {
      paddingHorizontal: 15,
      flexDirection: 'row', 
      alignItems: 'center',
      flex: 1, // para alinhar o ícone e a caixa de texto na mesma linha
      justifyContent: 'flex-start',
      borderRadius: 15,
      borderWidth: 1,
      height: 80,
      width: 330,
      backgroundColor: 'lightgrey',
      fontSize: 15,
      paddingVertical: 16,
      margin: 8
    },
    option2: {
      paddingHorizontal: 15,
      flexDirection: 'row', 
      flex: 1, // para alinhar o ícone e a caixa de texto na mesma linha
      justifyContent: 'space-between',
      alignItems: 'center',
      borderRadius: 15,
      borderWidth: 1,
      height: 50,
      width: 330,
      backgroundColor: 'lightgrey',
      fontSize: 15,
      paddingVertical: 16,
      margin: 8
    },
    option3: {
      paddingHorizontal: 15,
      flexDirection: 'row', 
      flex: 1, // para alinhar o ícone e a caixa de texto na mesma linha
      borderRadius: 15,
      borderWidth: 1,
      width: 330,
      backgroundColor: 'lightgrey',
      fontSize: 15,
      paddingVertical: 16,
      margin: 8
    },
    buttonBoxRight1: {
      position: 'absolute',
      bottom: 30,
      width: '100%',
      flexDirection: 'column',
      alignItems: 'center',
      borderWidth: 1,
      backgroundColor: 'lightgrey',
      borderRadius: 10,
      height: 50,
      width: 150,
      right: 15
    },
    buttonBackToList:   {
        position: 'absolute',
        bottom: 30,  
        width: '100%',
        flexDirection: 'row',
        alignItems: 'center',
        borderWidth: 1,
        backgroundColor: 'lightgrey',
        borderRadius: 10,
        height: 50,
        width: 330,
      },
  
    buttonToOptions: {
        position: 'absolute',
        bottom: 100,
        width: '100%',
        flexDirection: 'row',
        alignItems: 'center',
        borderWidth: 1,
        backgroundColor: 'lightgreen',
        borderRadius: 10,
        height: 50,
        width: 330,
      },
  
    buttonBoxLeft1: {
      position: 'absolute',
      bottom: 30,
      width: '100%',
      flexDirection: 'column',
      alignItems: 'center',
      borderWidth: 1,
      backgroundColor: 'lightgreen',
      borderRadius: 10,
      height: 50,
      width: 150,
      left: 15
    },

    buttonBoxRight2: {
        position: 'absolute',
        bottom: 30,
        width: '100%',
        flexDirection: 'column',
        alignItems: 'center',
        borderWidth: 1,
        backgroundColor: 'lightgreen',
        borderRadius: 10,
        height: 50,
        width: 150,
        right: 15
      },
    
      buttonBoxLeft2: {
        position: 'absolute',
        bottom: 30,
        width: '100%',
        flexDirection: 'column',
        alignItems: 'center',
        borderWidth: 1,
        backgroundColor: 'lightgrey',
        borderRadius: 10,
        height: 50,
        width: 150,
        left: 15
      },
    textsearchbar:{
      borderColor: 'transparent',
      fontSize: 15,
      paddingHorizontal: 35,
      height: 40, 
      width: 300,
      borderWidth: 0
    },
  
    searchbar: {
      width: 330,
      height: 40,
      borderRadius: 20,
      backgroundColor: 'lightgrey',
      borderWidth: 1,
      flexDirection: 'row', 
      alignItems: 'center',
      margin: 8,
    },
    border : {
      borderWidth: 1, // Largura da borda
      borderColor: 'black',
      borderRadius: 10, // para alinhar o ícone e a caixa de texto na mesma linha
      //alignItems: 'center', // para centralizar verticalmente
      height: 130,
      width: 330,
      margin: 8
    },

    border2 : {
        borderWidth: 1, // Largura da borda
        borderColor: 'black',
        borderRadius: 10, // para alinhar o ícone e a caixa de texto na mesma linha
        alignItems: 'center', // para centralizar verticalmente
        height: 70,
        width: 330,
        marginBottom: 30
      },
    title: {
      alignItems: 'center', // para centralizar verticalmente
      justifyContent: 'center',
      fontSize: 50,
      paddingVertical: 4,
    },
    titleBox: {
      flexDirection: 'row', // para alinhar o ícone e a caixa de texto na mesma linha
      alignItems: 'center', // para centralizar verticalmente
      justifyContent: 'flex-start',
      height: 100,
      width: '100%',
      paddingHorizontal: 30,
      paddingVertical: 80,
    },
    titleText: {
      flexDirection: 'column', // para alinhar o ícone e a caixa de texto na mesma linha
      alignItems: 'left', // para centralizar verticalmente
      justifyContent: 'flex-start',
      paddingHorizontal: 30,
      paddingVertical: 30,
    },
    subtitle: {
      flexDirection: 'column', // para alinhar o ícone e a caixa de texto na mesma linha
      alignItems: 'center', // para centralizar verticalmente
      justifyContent: 'center',
    },
    container: {
      flex: 1, // para alinhar o ícone e a caixa de texto na mesma linha
      alignItems: 'center', // para centralizar verticalmente
      justifyContent: 'flex-start',
    },
    box: {
      flexDirection: 'row', // para alinhar o ícone e a caixa de texto na mesma linha
      alignItems: 'center', // para centralizar verticalmente
      //justifyContent: 'left',
      height: 30,
      //width: '100%',
      //paddingHorizontal: 40

    },
    text: {
      left:15,
      fontSize: 18,
      marginBottom: 0,
    },
};

export default styles;  
