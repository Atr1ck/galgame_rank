import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query"
import { useState } from "react";

const queryCLient = new QueryClient();

function TopNavi({query, setQuery, searchBy, setSearchBy} : {query:string, setQuery: Function, searchBy:string, setSearchBy:Function}) {
    return (
        <div className="flex flex-row h-12 w-full rounded-lg bg-slate-50 shadow-md py-3 pl-40 justify-around">
            <div className="">
                11
            </div>
            <div>
                22
            </div>
            <SearchBar query={query} setQuery={setQuery} searchBy={searchBy} setSearchBy={setSearchBy}/>
        </div>
    )
}

function SearchBar({query, setQuery, searchBy, setSearchBy} : {query:string, setQuery: Function, searchBy:string, setSearchBy:Function}){
    const handleSearch = (e) => {
        const value = e.target.value;
        setQuery(value);
        console.log(query);
    }

    return (
        <div className="relative bottom-1 left-44">
            <select
            value={searchBy}
            onChange={(e) => setSearchBy(e.target.value)}
            className="p-1.5 border rounded-md"
            >
                <option value="name">游戏名</option>
                <option value="brand">会社</option>
            </select>
            <input
            type="text"
            value={query}
            onChange={handleSearch}
            placeholder="搜索..."
            className="p-1.5 border rounded-md">
            </input>
        </div>
    )
}

function Rank({ query, searchBy, page, limit} : {query:string, searchBy:string, page:number, limit:number}) {
    const { isPending, isError, data, error } = useQuery({
        queryKey:['games', query, searchBy],
        queryFn: async () => {
            const response = await fetch(
                `http://localhost:5000/data?query=${encodeURIComponent(query)}&searchBy=${searchBy}&page=${page}&limit=${limit}`,
            )
            
            return await response.json()
        }
    })

    if (isPending) {
        return <div>加载中...</div>;
    }
    
    if (isError) {
        return <div>加载错误: {error.message}</div>;
    }

    return (
        <div className="flex-grow border-2 border-black m-6 w-10/12 overflow-auto rounded-lg" >
            <table className="w-full">
                <thead>
                    <tr className="bg-gray-200 text-center">
                        <th className="px-4 py-2">排名</th>
                        <th className="px-4 py-2">游戏名</th>
                        <th className="px-4 py-2">封面</th>
                        <th className="px-4 py-2">会社</th>
                        <th className="px-4 py-2">中央值</th>
                        <th className="px-4 py-2">平均值</th>
                        <th className="px-4 py-2">标准偏差</th>
                        <th className="px-4 py-2">评论数</th>
                    </tr>
                </thead>
                <tbody className="text-center">
                {data.data.map(row => (
                    <tr className="border border-black" key={row.id}>
                        <td>{row.id}</td>
                        
                        <td className="max-w-14">
                            <a className="hover:text-red-600" href={row.game_link} target="_blank" rel="noopener noreferrer">
                                {row.game_name}
                            </a>
                        </td>
                        
                        <td className="text-center">
                            <img className="w-32 h-auto mx-auto my-2" src={row.img_link} alt={row.game_name} />
                        </td>
                        
                        <td>
                            <a href={row.brand_link} target="_blank" rel="noopener noreferrer">
                                {row.brand_name}
                            </a>
                        </td>
                        
                        <td>{row.medium_value}</td>
                        
                        <td>{row.average_value}</td>
                        
                        <td>{row.standard_deviation}</td>
                        
                        <td>{row.comments}</td>
                    </tr>
        ))}
                </tbody>
            </table>
        </div>
        
    )
}

export default function Home(){
    const [query, setQuery] = useState("");
    const [searchBy, setSearchBy] = useState("name");

    return (
        <div className="flex flex-col h-screen items-center">
        <TopNavi query={query} setQuery={setQuery} searchBy={searchBy} setSearchBy={setSearchBy}/>
        <QueryClientProvider client={queryCLient}>
        <Rank query={query} searchBy={searchBy} page={1} limit={200}></Rank>
        </QueryClientProvider>
        </div>
    )
}