## Shop Smart interface

### Install npm

#### For Linux users

```bash
sudo apt-get install nodejs npm
```

#### For Windows users

Download on web site and follow instructions

```bash
 https://nodejs.org/
```

#### Verify version

```bash
node -v
npm -v
```

### Create a folder to project

```bash
mkdir interface
cd interface
```

### To clone this repo

```bash
git clone https://github.com/SteliosKarvanis/ShopSmart
```

```bash
git checkout frontend/b
```

### Install requirements

```bash
cd ShopSmart/front-end
```

Go to front-end project root, where are .js files and run the following commands

```bash
npm install
npx expo install react-native-web@~0.19.6 react-dom@18.2.0
npm install react-native-screens react-native-safe-area-context
npm install @react-navigation/native
npm install @react-navigation/stack
npm install react-native-vector-icons --save
npx expo install --fix
npm install @react-native-community/geolocation --save
```

### Run interface

```bash
npm start
```

## OBS: 

When commiting or pushing go to repo root /ShopSmart

### Simulator extection

```bash
https://chrome.google.com/webstore/detail/mobile-simulator-responsi/ckejmhbmlajgoklhgbapkiccekfoccmk/related?hl=fr
```
