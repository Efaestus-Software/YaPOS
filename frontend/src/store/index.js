import {createStore} from 'vuex'
import {getAPI} from '../axios-api'
import createPersistedState from 'vuex-persistedstate'

export default createStore({
    plugins: [createPersistedState({
        storage: window.localStorage,
    })],

    state: {
        accessToken: null,
        refreshToken: null,
        APIData: null,
        activeNav: null,
        lastStableNav: null,
        myDetails: {
            username: null,
            first_name: null,
            last_name: null,
            is_superuser: null,
        }
    },

    mutations: {
        updateStorage(state, { access, refresh }){
            state.accessToken = access
            state.refreshToken = refresh
        },

        updateMyDetails(state, details){

            state.myDetails.username = details.username
            state.myDetails.first_name = details.first_name
            state.myDetails.last_name = details.last_name
            state.myDetails.is_superuser = details.is_superuser
        },

        refreshAccessToken(state, accessToken){
            state.accessToken = accessToken
        },

        changeLastStableNav(state, id){
            state.lastStableNav = id
        },
    },

    getters: {
        loggedIn(state){
            return state.accessToken != null
        },
        is_superuser(state){
            return state.is_superuser
        }
    },

    actions: {
        async userLogin(context, usercredentials){
            await new Promise((resolve, reject)=>{
                getAPI.post('/api/token/', {
                    username: usercredentials.username,
                    password: usercredentials.password
                })
                .then(res => {
                    context.commit('updateStorage', {access: res.data.access, refresh: res.data.refresh})
                    let details = {}
                    getAPI.get('/me/', {
                        headers: {
                            Authorization: `Bearer ${context.accessToken}`
                        }
                    })
                    .then(res=>{
                        details = res.data
                        context.commit('updateMyDetails', details)
                    })
                    resolve()
                })
                .catch(err=>{
                    console.log('store', err)
                    reject(err)
                })
            })
        },

        userLogout(context){
            if (context.getters.loggedIn){
                context.state.accessToken = null
                context.state.refreshToken = null
                context.state.currentNav = 'home'
                context.state.currentSubNav = ''
                localStorage.clear();
            }
        }
    },
    
    modules: {
        
    }
})