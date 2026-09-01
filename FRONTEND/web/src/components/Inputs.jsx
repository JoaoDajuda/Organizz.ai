import React, { Children } from 'react'

const ModalStyle = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        zIndex: 1000,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    ContainerPrincipal: {
        backgroundColor: '#706f6f',
        borderRadius: '12px',
        padding: '32px',
        width: '90%',
        maxWidth: '400px',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.3)',
    },
}

export default function Inputs({}) {
    
}