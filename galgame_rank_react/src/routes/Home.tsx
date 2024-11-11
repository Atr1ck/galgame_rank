import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query"
import { useState } from "react";

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

interface Game {
    id: number,
    game_link: string,
    img_link: string,
    game_name: string,
    brand_name: string,
    brand_link: string,
    medium_value: number,
    average_value: number,
    standard_deviation: number,
    comments: number 
}

interface ApiResponse<T> {
    data: T[];       // rows 数据的类型，假设为泛型数组
    total_pages: number;  // 总页数
}

function Rank({query, searchBy, page, setTotalpages}: {query: string, searchBy:string,page: number, setTotalpages:Function}) {
    const { isPending, isError, data, error } = useQuery({
        queryKey:['games', query, searchBy, page],
        queryFn: async () => {
            const response = await fetch(
                `http://localhost:5000/data?query=${encodeURIComponent(query)}&searchBy=${searchBy}&page=${page}&limit=${30}`,
            )
            
            return await response.json()
        }
    })

    if (isPending) {
        return <div className="border-2 border-black m-6 w-10/12 h-5/6 overflow-auto rounded-lg">
            加载中...
        </div>
    }
    
    if (isError) {
        return <div>加载错误: {error.message}</div>;
    }

    setTotalpages(data.total_pages);

    return (
        <div className="border-2 border-black m-6 w-10/12 h-5/6 overflow-auto rounded-lg shadow-md" >
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
                {data.data.map((row)=> (
                    <tr className="border-y border-black" key={row.id}>
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

function FbButton({handleforward, handlebackward, isBackwardDisabled, isForwardDisabled}
    :{handleforward:() => void, handlebackward:() =>void, isBackwardDisabled:boolean, isForwardDisabled: boolean}){
    
    return(
    <div className="flex justify-center gap-x-9 w-10/12">
        <button className="border-2 border-black rounded-lg w-36 h-auto p-2" onClick={handlebackward} disabled={isBackwardDisabled}>
            上一页
        </button>
        <button className="border-2 border-black rounded-lg w-36 h-auto p-2" onClick={handleforward} disabled={isForwardDisabled}>
            下一页
        </button>
    </div>
    )
}

export default function Home(){
    const [query, setQuery] = useState("");
    const [searchBy, setSearchBy] = useState("name");
    const [page, setPage] = useState(1);
    const [isForwardDisabled, setIsForwardDisabled] = useState(false);
    const [isBackwardDisabled, setIsBackwardDisabled] = useState(true);
    const [total_pages, setTotalpages] = useState(1);

    const handleforward = () => {
        setPage((prevPage) => {
            const newPage = prevPage + 1;
            setIsBackwardDisabled(false); // 前进后上一页按钮可以启用
            if (newPage === total_pages) {
                setIsForwardDisabled(true); // 达到最大页数时禁用下一页按钮
            }
            return newPage;
        });
    };

    const handlebackward = () => {
        setPage((prevPage) => {
            const newPage = prevPage - 1;
            setIsForwardDisabled(false); // 回退后下一页按钮可以启用
            if (newPage === 1) {
                setIsBackwardDisabled(true); // 到第一页时禁用上一页按钮
            }
            return newPage;
        });
    };

    return (
        <div className="flex flex-col h-screen items-center">
            <TopNavi query={query} setQuery={setQuery} searchBy={searchBy} setSearchBy={setSearchBy}/>
            <Rank page={page} query={query} searchBy={searchBy} setTotalpages={setTotalpages}></Rank>
            <FbButton handlebackward={handlebackward} handleforward={handleforward}
            isBackwardDisabled={isBackwardDisabled} isForwardDisabled={isForwardDisabled}></FbButton>
        </div>
    )
}   