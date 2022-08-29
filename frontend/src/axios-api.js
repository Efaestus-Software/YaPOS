import axios from 'axios'
import store from './store/index'

const getAPI = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        Authorization: `Bearer ${store.state.accessToken}`
    }
})

getAPI.interceptors.response.use(
    (res)=>{
        return res
    },
    
    async (err)=>{
        const originalConfig = err.config
        if(err.response.status == 401 && originalConfig.url !== '/api/token/refresh/' && !originalConfig._retry){
            originalConfig._retry = true
            try{
                const rs = await getAPI.post('/api/token/refresh/', {
                    refresh: store.state.refreshToken
                })

                console.log('accessToken is saved')
                const accessToken = rs.data.access;
                store.commit('refreshAccessToken', accessToken)
                originalConfig.headers['Authorization'] = `Bearer ${accessToken}`

                console.log('returns Original Config')
                return getAPI(originalConfig)

            } catch(_error){
                return Promise.reject(_error);
            }
        } else {
            console.log('STATUS NOT 401 OR ORIGINAL CONFIG IS RETRY')
        }

        return Promise.reject(err)
    })

export { getAPI }