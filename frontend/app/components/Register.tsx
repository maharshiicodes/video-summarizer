'use client'
import { useState } from "react"
import { API_URL } from "../lib/api";
import axios from 'axios'
import Spinner from '@/app/components/Spinner'

interface RegisterProps{
  username: string;
  email: string;
  password: string;
}
export default function Login() {
  const [form, setForm] = useState<RegisterProps>({ 'username' : '', 'email': '', 'password': '' })
  const [submitting, setSubmitting] = useState<boolean>(false);

  async function handleSubmit(e : React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await axios.post(`${API_URL}/register`, {
        body : form
      })
    } catch (e) {
      console.log(e)
    } finally {
      setSubmitting(false);
    }
    
  }
  
  return (
    <div className="w-full min-h-screen flex items-center justify-center bg-neutral-50">
      <form className="bg-white flex flex-col items-start gap-4 p-20 border border-neutral-300 border-2 w-100 h-140 rounded-xl hover:rounded-3xl shadow-md shadow-neutral-800 transition-all ease-out">
        <div className = ''>
          <h1 className = 'font-manrope text-2xl text-neutral-800'>create an account</h1>
        </div>
        <div className="flex flex-col gap-2 ">
          <label className='font-manrope text-neutral-800 text-md'>username</label>
          <input type="text" placeholder="enter your name" className="placeholder:text-neutral-400 border border-neutral-300 rounded-md p-2 focus:outline-none focus:border-neutral-400 text-neutral-800 font-manrope"
            onChange={ (e) => setForm({...form,username : e.target.value})} />
        </div>
        <div className="flex flex-col gap-2 ">
          <label className='font-manrope text-neutral-800 text-md'>email</label>
          <input type="email" placeholder="enter your email" className="placeholder:text-neutral-400 border border-neutral-300 rounded-md p-2 focus:outline-none focus:border-neutral-400 text-neutral-800 font-manrope"
            onChange={ (e) => setForm({...form,email : e.target.value})} />
        </div>
        <div className="flex flex-col gap-2">
          <label className='font-manrope text-black text-md'>password</label>
          <input type="password" placeholder="enter your password" className="placeholder:text-neutral-400 border border-neutral-300 rounded-md p-2 focus:outline-none focus:border-neutral-400 text-neutral-800 font-manrope"
          onChange={ (e) => setForm({...form,password : e.target.value})}/>
        </div>
        <div className="bg-neutral-800 p-1 flex items-center justify-center rounded-sm">
          <button
            onClick={handleSubmit}
            className="w-55 bg-neutral-800 h-10 rounded-sm border border-neutral-600 active:scale-99 transition-all ease-out"
          >
            <div className="font-manrope text-white text-center cursor-pointer">{submitting ? <div className = 'flex items-center justify-center'><Spinner/></div> : 'register'}</div>
          </button>
        </div>
        <div className = ''>
          <p className = 'text-neutral-500 text-center font-manrope'>already have an account? <a className = 'text-black cursor-pointer border-b border-neutral-400' href='/login'>login</a></p>
        </div>
      </form>
    </div>
  )
}