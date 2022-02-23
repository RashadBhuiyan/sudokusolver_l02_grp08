import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import styled from 'styled-components'
import styles from '../styles/Home.module.css'
import Layout from './components/layout'

const Body = styled.div`
  height: 100vh;
  width: 100vw;
`;

const Home: NextPage = () => {
  return (
    <Layout>
      <Body>

      </Body>
    </Layout>
  )
}

export default Home
