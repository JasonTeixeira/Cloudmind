export const BrowserRouter = ({ children }: { children: any }) => children
export const Routes = ({ children }: { children: any }) => children
export const Route = ({ children }: { children: any }) => children
export const Link = ({ children }: { children: any }) => children
export const useNavigate = () => jest.fn()
export const useParams = () => ({} as Record<string, string>)
export const useLocation = () => ({ pathname: '/', search: '', hash: '' })




